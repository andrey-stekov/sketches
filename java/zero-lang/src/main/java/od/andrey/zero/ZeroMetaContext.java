package od.andrey.zero;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:21 PM
 * To change this template use File | Settings | File Templates.
 */
public interface ZeroMetaContext {
    <T> T getValue(int ind);
    <T> int  addValue(T value);
    <T> void setValue(int ind, T value);
    void remValue(int ind);

    void addWord(KeyWord keyWord, Word word);
    Word getWord(KeyWord keyWord);
    void remWord(KeyWord keyWord);
}
