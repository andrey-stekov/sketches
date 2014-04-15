package od.andrey.zero;

/**
 * Created with IntelliJ IDEA.
 * User: ALemeshev
 * Date: 15.04.14
 * Time: 18:44
 * To change this template use File | Settings | File Templates.
 */
public class KeyWord {
    private String k;

    public KeyWord(String k) {
        this.k = k.toUpperCase();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        KeyWord keyWord = (KeyWord) o;

        return !(k != null ? !k.equals(keyWord.k) : keyWord.k != null);

    }

    @Override
    public int hashCode() {
        return k != null ? k.hashCode() : 0;
    }

    @Override
    public String toString() {
        return k;
    }
}
