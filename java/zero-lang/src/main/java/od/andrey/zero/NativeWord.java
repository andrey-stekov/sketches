package od.andrey.zero;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:15 PM
 * To change this template use File | Settings | File Templates.
 */
public interface NativeWord extends Word {
    void execute(ZeroContext context, ZeroExecutor executor);
}
