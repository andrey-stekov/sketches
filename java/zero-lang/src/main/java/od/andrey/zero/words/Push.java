package od.andrey.zero.words;

import od.andrey.zero.KeyWord;
import od.andrey.zero.NativeWord;
import od.andrey.zero.ZeroContext;
import od.andrey.zero.ZeroExecutor;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:52 PM
 * To change this template use File | Settings | File Templates.
 */
public class Push implements NativeWord {
    public static final KeyWord KEY_WORD = new KeyWord("push");

    @Override
    public void execute(ZeroContext context, ZeroExecutor executor) {
        Object[] params = context.<Object[]>stackPop();

        assert params.length > 0;

        Object val = params[0];
        context.stackPush(val);
        context.incPC();
    }

    @Override
    public KeyWord getKeyWord() {
        return KEY_WORD;
    }
}