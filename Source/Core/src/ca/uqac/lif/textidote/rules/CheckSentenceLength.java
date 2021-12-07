package ca.uqac.lif.textidote.rules;

import com.googlecode.jsonrpc4j.JsonRpcServer;

import java.util.ArrayList;
import java.util.List;

import ca.uqac.lif.textidote.Advice;
import ca.uqac.lif.textidote.Rule;
import ca.uqac.lif.textidote.as.AnnotatedString;

public class CheckSentenceLength extends Rule
{
   public CheckSentenceLength()
   {
      super("sh:capperiod");
   }

   @Override
   public List<Advice> evaluate(AnnotatedString s, AnnotatedString original)
   {
      JsonRpcServer server;// = new JsonRpcServer(userService, UserService.class);
      List<Advice> out_list = new ArrayList<Advice>();
      // The question is is there a way to configure the rule? then one could configure the path to the tools
      // Add `dict` and `style` support
      System.out.println("COMING HERE");

      return out_list;
   }

   @Override
   public String getDescription()
   {
      return "Too long sentences are not appropriate for scientific writing.";
   }
}
