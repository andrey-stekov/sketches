package od.andrey.zero;

import od.andrey.zero.words.*;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.StringReader;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: ALemeshev
 * Date: 15.04.14
 * Time: 18:39
 * To change this template use File | Settings | File Templates.
 */
public class Zero implements ZeroMetaContext, ZeroExecutor {
    private Map<KeyWord, Word> words = new ConcurrentHashMap<KeyWord, Word>();
    private List<Value> values = new CopyOnWriteArrayList<Value>();

    {
        words.put(Out.KEY_WORD,     new Out());
        words.put(Push.KEY_WORD,    new Push());
        words.put(Add.KEY_WORD,     new Add());
    }

    @Override
    public <T> T getValue(int ind) {
        Value v = values.get(ind);

        if (v == null) {
            throw new IllegalStateException("Value was removed.");
        }

        return (T) v.getVal();
    }

    @Override
    public <T> int addValue(T value) {
        Value<T> v = new Value<T>(value);
        values.add(v);
        return values.indexOf(v);
    }

    @Override
    public <T> void setValue(int ind, T value) {
        Value v = values.get(ind);

        if (v == null) {
            throw new IllegalStateException("Value was removed.");
        }

        v.setVal(value);
    }

    @Override
    public void remValue(int ind) {
        values.set(ind, null);
    }

    @Override
    public void addWord(KeyWord keyWord, Word word) {
        words.put(keyWord, word);
    }

    @Override
    public Word getWord(KeyWord keyWord) {
        Word w = words.get(keyWord);

        if (w == null) {
            throw new IllegalStateException("Word was removed.");
        }

        return w;
    }

    @Override
    public void remWord(KeyWord keyWord) {
        words.remove(keyWord);
    }

    public void execute(List<Word> words, ZeroContext context, ZeroExecutor executor) {
        while (context.getPC() < words.size()) {
            execute(words.get(context.getPC()), context, executor);
        }
    }

    @Override
    public void execute(Word word, ZeroContext context, ZeroExecutor executor) {
        if (word instanceof WordWithParams) {
            context.stackPush(((WordWithParams) word).getParams());
            word = ((WordWithParams) word).getWord();
        }

        if (word instanceof UserDefinedWord) {
            context.pushPC();
            execute(((UserDefinedWord) word).getWords(), context, executor);
            context.popPC();
            context.incPC();
        } else if (word instanceof NativeWord) {
            ((NativeWord) word).execute(context, executor);
        } else {
            throw new IllegalArgumentException("Incorrect word: " + word);
        }
    }

    @Override
    public void execute(String code, InputStream is, OutputStream os) {
        String[] tokens = code.split("[\\s]+");

        List<Word> words = new ArrayList<Word>(tokens.length);

        for (String t : tokens) {
            Integer i = null;

            try {
                i = Integer.parseInt(t);
            } catch (Exception ignored) { }

            if (i != null) {
                words.add(new WordWithParams(this.words.get(Push.KEY_WORD), i));
            } else {
                KeyWord keyWord = new KeyWord(t);
                Word word = this.words.get(keyWord);

                if (word == null) {
                    throw new IllegalArgumentException("Illegal word: " + t);
                }

                words.add(word);
            }
        }

        execute(words, new ContextImpl(this, is, os), this);
    }
}
