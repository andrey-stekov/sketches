package od.andrey.zero;

import java.io.InputStream;
import java.io.OutputStream;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 8:46 PM
 * To change this template use File | Settings | File Templates.
 */
public interface ZeroExecutor {
    void execute(Word word, ZeroContext context, ZeroExecutor executor);
    void execute(String code, InputStream is, OutputStream os);
}
