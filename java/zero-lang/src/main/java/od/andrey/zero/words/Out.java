package od.andrey.zero.words;

import od.andrey.zero.KeyWord;
import od.andrey.zero.NativeWord;
import od.andrey.zero.ZeroContext;
import od.andrey.zero.ZeroExecutor;

import java.io.PrintWriter;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:48 PM
 * To change this template use File | Settings | File Templates.
 */
public class Out implements NativeWord {
    public static final KeyWord KEY_WORD = new KeyWord("out");

    @Override
    public void execute(ZeroContext context, ZeroExecutor executor) {
        Object v = context.stackPop();
        new PrintWriter(context.getOutputStream()).append(v.toString()).flush();
        context.incPC();
    }

    @Override
    public KeyWord getKeyWord() {
        return KEY_WORD;
    }
}
