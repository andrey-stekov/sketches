package od.andrey.zero.words;

import od.andrey.zero.KeyWord;
import od.andrey.zero.NativeWord;
import od.andrey.zero.ZeroContext;
import od.andrey.zero.ZeroExecutor;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 10:07 PM
 * To change this template use File | Settings | File Templates.
 */
public class Add implements NativeWord {
    public static final KeyWord KEY_WORD = new KeyWord("+");

    @Override
    public void execute(ZeroContext context, ZeroExecutor executor) {
        Integer b = context.<Integer>stackPop();
        Integer a = context.<Integer>stackPop();
        context.<Integer>stackPush(a + b);
        context.incPC();
    }

    @Override
    public KeyWord getKeyWord() {
        return KEY_WORD;
    }
}