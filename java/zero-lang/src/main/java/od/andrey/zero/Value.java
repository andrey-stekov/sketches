package od.andrey.zero;

/**
 * Created with IntelliJ IDEA.
 * User: ALemeshev
 * Date: 15.04.14
 * Time: 18:40
 * To change this template use File | Settings | File Templates.
 */
public class Value<T> {
    private T val;

    public Value(T val) {
        this.val = val;
    }

    public T getVal() {
        return val;
    }

    public void setVal(T val) {
        this.val = val;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Value value = (Value) o;

        return !(val != null ? !val.equals(value.val) : value.val != null);

    }

    @Override
    public int hashCode() {
        return val != null ? val.hashCode() : 0;
    }

    @Override
    public String toString() {
        return val == null ? "null" : "class = " + val.getClass() + "val = " + val;
    }
}
