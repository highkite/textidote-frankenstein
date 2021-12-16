package ca.uqac.lif.textidote.rules;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StringWriter;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.lang.InterruptedException;

import com.googlecode.jsonrpc4j.JsonRpcServer;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;
import org.json.simple.parser.JSONParser;

import java.util.ArrayList;
import java.util.List;
import java.io.IOException;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.thetransactioncompany.jsonrpc2.server.*;

import javax.net.ServerSocketFactory;
import com.googlecode.jsonrpc4j.StreamServer;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.InetAddress;

import ca.uqac.lif.textidote.Advice;
import ca.uqac.lif.textidote.Rule;
import ca.uqac.lif.textidote.as.AnnotatedString;
import ca.uqac.lif.textidote.as.Position;
import ca.uqac.lif.textidote.as.Range;

interface LinterService {
   /**
    * Returns all the lines
    * */
   public List<String> getLines();

   /**
    * Returns the line at the given index
    * 0 <= index < getLineCount()
    * */
   public String getLine(int index);

   /**
    * Give advice to a certain line
    * */
   public void setAdvice(int index, String advice, int start_pos, int end_pos);

   /**
    * Returns the number of available lines
    * */
   public int getLineCount();
}

class LinterServiceImpl implements LinterService {
   private List<Advice> out_list = new ArrayList<Advice>();
   private List<String> lines;
   private AnnotatedString original;
   private AnnotatedString s;
   private Rule rule;

   public LinterServiceImpl(Rule rule, AnnotatedString s, AnnotatedString original) {
      this.rule = rule;
      this.lines = s.getLines();
      this.original = original;
      this.s = s;
   }

   /**
    * Returns all the lines
    * */
   public List<String> getLines() {
      return this.lines;
   }

   /**
    * Returns the line at the given index
    * 0 <= index < getLineCount()
    * */
   public String getLine(int index) {
      return this.lines.get(index);
   }

   /**
    * Give advice to a certain line
    * */
   public void setAdvice(int index, String advice, int start_pos, int end_pos) {
      Position start_p = this.s.getSourcePosition(new Position(index, start_pos));
      Position end_p = this.s.getSourcePosition(new Position(index, end_pos));
      Range r = new Range(start_p, end_p);
      this.out_list.add(new Advice(this.rule, r, advice, this.original.getResourceName(), this.original.getLine(index), this.original.getOffset(start_p)));
   }

   /**
    * Returns the number of available lines
    * */
   public int getLineCount() {
      return this.lines.size();
   }

   List<Advice> getAdviceList() {
      return this.out_list;
   }
}

public class JSONRpcServer extends Rule
{
   private AtomicBoolean atomicServerShutdown = new AtomicBoolean(false);

   public JSONRpcServer ()
   {
      super("sh:jsonrpc");
   }

   static class LintHandler implements HttpHandler {
      private LinterService linterService;
      private AtomicBoolean atomicServerShutdown;

      public LintHandler(LinterService linterService, AtomicBoolean atomicServerShutdown) {
	 this.linterService = linterService;
	 this.atomicServerShutdown = atomicServerShutdown;
      }

      @Override
      public void handle(HttpExchange t) throws IOException {
	 OutputStream os = t.getResponseBody();
	 InputStreamReader isr =  new InputStreamReader(t.getRequestBody(),"utf-8");
	 BufferedReader br = new BufferedReader(isr);
	 String s = br.readLine();
	 JSONParser parser = new JSONParser();
	 JSONObject ret_obj = new JSONObject();
	 try{
	    JSONObject obj = (JSONObject)parser.parse(s);
	    System.out.println(obj.get("method"));
	    ret_obj.put("id", obj.get("id"));
	    ret_obj.put("jsonrpc", "2.0");
	    if(obj.get("method").equals("getLines")) {
	       JSONArray ret_vals = new JSONArray();
	       for(int i = 0; i < this.linterService.getLineCount(); i++) {
		  ret_vals.add(this.linterService.getLine(i));
	       }
	       ret_obj.put("result", ret_vals);
	    } else if (obj.get("method").equals("getLine")) {
	       JSONArray params = (JSONArray)obj.get("params");
	       int index = ((java.lang.Long) params.get(0)).intValue();
	       ret_obj.put("result", this.linterService.getLine(index));
	    } else if (obj.get("method").equals("setAdvice")) {
	       JSONArray params = (JSONArray)obj.get("params");
	       int index = ((java.lang.Long) params.get(0)).intValue();
	       String advice = (String)params.get(1);
	       int start_pos = ((java.lang.Long) params.get(2)).intValue();
	       int end_pos = ((java.lang.Long) params.get(3)).intValue();
	       this.linterService.setAdvice(index, advice, start_pos, end_pos);
	       ret_obj.put("result", "Advice set");
	    } else if (obj.get("method").equals("getLineCount")) {
	       ret_obj.put("result", new Integer(this.linterService.getLineCount()));
	    } else if (obj.get("method").equals("completeCheck")) {
	       atomicServerShutdown.set(true);
	       ret_obj.put("result", "Check completed; shutdown server");
	    }
	    StringWriter out = new StringWriter();
	    ret_obj.writeJSONString(out);
	    String response = out.toString();
	    t.sendResponseHeaders(200, response.length());

	    os.write(response.getBytes());
	    os.close();
	 }catch(ParseException ex) {
	    System.out.println(ex);
	 }
      }
   }

   @Override
   public List<Advice> evaluate(AnnotatedString s, AnnotatedString original)
   {
      LinterServiceImpl linterService = new LinterServiceImpl(this, s, original);
      System.out.println("Starting JSON RPC server");

      HttpServer server = null;
      try {
	 server = HttpServer.create(new InetSocketAddress(8888), 0);
	 server.createContext("/textidote", new LintHandler(linterService, this.atomicServerShutdown));
	 server.setExecutor(null); // creates a default executor
	 server.start();
      } catch(IOException ex) {
	 System.out.println(ex);
      }
      List<Advice> out_list = new ArrayList<Advice>(); //linterService.getAdviceList();
      while(!this.atomicServerShutdown.get()) {
	 try {
	    TimeUnit.SECONDS.sleep(1);
	 } catch (InterruptedException ex) {
	    System.out.println(ex);
	 }
      }

      System.out.println("Shutdown JSONRpcServer...");
      server.stop(2);
      System.out.println("continue execution");

      out_list = linterService.getAdviceList();

      return out_list;
   }

   @Override
   public String getDescription()
   {
      return "Opens a JSON RPC server to serve stripped text to for instance NLTK processors or whatever";
   }
}
