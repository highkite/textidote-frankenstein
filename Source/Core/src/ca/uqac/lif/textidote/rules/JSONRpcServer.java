package ca.uqac.lif.textidote.rules;
import java.io.BufferedReader;
import java.io.InputStreamReader;

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
   public void setAdvice(int index, String advice);

   /**
    * Returns the number of available lines
    * */
   public int getLineCount();

   /**
    * Terminate the check and let textidote continue doing its thing
    * */
   public void completeCheck();
}

class LinterServiceImpl implements LinterService {
   private List<Advice> out_list = new ArrayList<Advice>();
   /**
    * Returns all the lines
    * */
   public List<String> getLines() {
      List<String> ret_val = new ArrayList<String>();
      return ret_val;
   }

   /**
    * Returns the line at the given index
    * 0 <= index < getLineCount()
    * */
   public String getLine(int index) {
      return "";
   }

   /**
    * Give advice to a certain line
    * */
   public void setAdvice(int index, String advice) {
   }

   /**
    * Returns the number of available lines
    * */
   public int getLineCount() {
      return 0;
   }

   /**
    * Terminate the check and let textidote continue doing its thing
    * */
   public void completeCheck() {
   }

   List<Advice> getAdviceList() {
      return this.out_list;
   }
}

public class JSONRpcServer extends Rule
{

   // Implements a handler for an "echo" JSON-RPC method
   //public static class EchoHandler implements RequestHandler {


   //   // Reports the method names of the handled requests
   //   public String[] handledRequests() {

   //      return new String[]{"echo"};
   //   }


   //   // Processes the requests
   //   public JSONRPC2Response process(JSONRPC2Request req, MessageContext ctx) {

   //      if (req.getMethod().equals("echo")) {

   //         // Echo first parameter

   //         List params = (List)req.getParams();

   //         Object input = params.get(0);

   //         return new JSONRPC2Response(input, req.getID());
   //      }
   //      else {

   //         // Method name not supported

   //         return new JSONRPC2Response(JSONRPC2Error.METHOD_NOT_FOUND, req.getID());
   //      }
   //   }
   //}

   public JSONRpcServer ()
   {
      super("sh:jsonrpc");
   }

   static class MyHandler implements HttpHandler {
      //   private Dispatcher dispatcher;
      //   public MyHandler(Dispatcher dispatcher) {
      //      this.dispatcher = dispatcher;
      //   }
      @Override
      public void handle(HttpExchange t) throws IOException {
	 String response = "This is the response";
	 t.sendResponseHeaders(200, response.length());
	 OutputStream os = t.getResponseBody();
	 InputStreamReader isr =  new InputStreamReader(t.getRequestBody(),"utf-8");
	 BufferedReader br = new BufferedReader(isr);
	 String s = br.readLine();
	 JSONParser parser = new JSONParser();
	 try{
	    JSONObject obj = (JSONObject)parser.parse(s);
	    System.out.println(obj.get("method"));
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
      LinterServiceImpl linterService = new LinterServiceImpl();
      List<String> lines = s.getLines();
      System.out.println("Starting JSON RPC server");

      // Create a new JSON-RPC 2.0 request dispatcher
      //      Dispatcher dispatcher =  new Dispatcher();
      //
      //
      //      // Register the "echo", "getDate" and "getTime" handlers with it
      //      dispatcher.register(new EchoHandler());
      HttpServer server;
      try {
	 server = HttpServer.create(new InetSocketAddress(8888), 0);
	 server.createContext("/test", new MyHandler());
	 server.setExecutor(null); // creates a default executor
	 server.start();
      } catch(IOException ex) {
	 System.out.println(ex);
      }
      List<Advice> out_list = new ArrayList<Advice>(); //linterService.getAdviceList();
      boolean atomicServerShutDown = false;
      while(!atomicServerShutDown);

      //      JsonRpcServer server = new JsonRpcServer(linterService, LinterService.class);
      //
      //      ServerSocket socket;
      //      try {
      //	 socket = ServerSocketFactory.getDefault().createServerSocket(8888);
      //      } catch (IOException exception) {
      //	 System.out.println("Could not create server socket");
      //	 return new ArrayList<Advice>();
      //      }
      //
      //      StreamServer streamServer = new StreamServer(server, 5, socket);

      //      streamServer.start();
      //
      //      while(streamServer.isStarted());


      return out_list;
   }

   @Override
   public String getDescription()
   {
      return "Opens a JSON RPC server to serve stripped text to for instance NLTK processors or whatever";
   }
}
