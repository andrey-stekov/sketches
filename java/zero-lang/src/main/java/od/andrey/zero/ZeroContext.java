package od.andrey.zero;

import java.io.InputStream;
import java.io.OutputStream;

/**
 * Created with IntelliJ IDEA.
 * User: ALemeshev
 * Date: 15.04.14
 * Time: 18:48
 * To change this template use File | Settings | File Templates.
 */
public interface ZeroContext extends ZeroMetaContext {
    void incPC();
    void addPC(int offset);
    int  getPC();
    void pushPC();
    void popPC();

    <T> void stackPush(T value);
    <T> T stackPop();
    <T> T stackPeek();

    InputStream getInputStream();
    OutputStream getOutputStream();
}
