package od.andrey.zero;

import java.io.InputStream;
import java.io.OutputStream;
import java.util.Deque;
import java.util.LinkedList;

/**
 * Created with IntelliJ IDEA.
 * User: andrey
 * Date: 4/15/14
 * Time: 9:35 PM
 * To change this template use File | Settings | File Templates.
 */
public class ContextImpl implements ZeroContext {
    private Deque<Integer> callStack;
    private Deque stack;
    private Zero z;
    private int pc;

    InputStream is;
    OutputStream os;

    public ContextImpl(Zero z, InputStream is, OutputStream os) {
        this.z = z;
        this.pc = 0;
        this.is = is;
        this.os = os;
        this.callStack = new LinkedList<Integer>();
        this.stack = new LinkedList();
    }

    @Override
    public <T> T getValue(int ind) {
        return z.<T>getValue(ind);
    }

    @Override
    public <T> int addValue(T value) {
        return z.<T>addValue(value);
    }

    @Override
    public <T> void setValue(int ind, T value) {
        z.<T>setValue(ind, value);
    }

    @Override
    public void remValue(int ind) {
        z.remValue(ind);
    }

    @Override
    public void addWord(KeyWord keyWord, Word word) {
        z.addWord(keyWord, word);
    }

    @Override
    public Word getWord(KeyWord keyWord) {
        return z.getWord(keyWord);
    }

    @Override
    public void remWord(KeyWord keyWord) {
        z.remWord(keyWord);
    }

    @Override
    public void incPC() {
        pc++;
    }

    @Override
    public void addPC(int offset) {
        pc += offset;
    }

    @Override
    public int getPC() {
        return pc;
    }

    @Override
    public void pushPC() {
        callStack.push(pc);
        pc = 0;
    }

    @Override
    public void popPC() {
        if (callStack.isEmpty()) {
            throw new IllegalStateException("Call stack is empty.");
        }

        pc = callStack.pop();
    }

    @Override
    public <T> void stackPush(T value) {
        stack.push(value);
    }

    @Override
    public <T> T stackPop() {
        if (stack.isEmpty()) {
            throw new IllegalStateException("Stack is empty.");
        }

        return (T) stack.pop();
    }

    @Override
    public <T> T stackPeek() {
        if (stack.isEmpty()) {
            throw new IllegalStateException("Stack is empty.");
        }

        return (T) stack.peek();
    }

    @Override
    public InputStream getInputStream() {
        return is;
    }

    @Override
    public OutputStream getOutputStream() {
        return os;
    }
}