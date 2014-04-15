package od.andrey.zero;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:38 PM
 * To change this template use File | Settings | File Templates.
 */
public class WordWithParams implements Word {
    public static final Object[] EMPTY_PARAMS = new Object[0];

    private Word word;
    private Object[] params;

    public WordWithParams(Word word, Object... params) {
        this.word = word;
        this.params = params;
    }

    public WordWithParams(Word word) {
        this.word = word;
        this.params = EMPTY_PARAMS;
    }

    public Word getWord() {
        return word;
    }

    public Object[] getParams() {
        return params;
    }

    @Override
    public KeyWord getKeyWord() {
        return word.getKeyWord();
    }
}
