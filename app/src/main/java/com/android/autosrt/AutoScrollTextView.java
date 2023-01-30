package com.android.autosrt;

import android.content.Context;
import android.text.Editable;
import android.text.Selection;
import android.text.Spannable;
import android.text.method.MovementMethod;
import android.text.method.ScrollingMovementMethod;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.accessibility.AccessibilityEvent;
import android.widget.TextView;

import androidx.appcompat.widget.AppCompatEditText;

import java.util.Objects;

public class AutoScrollTextView extends AppCompatEditText {
    public AutoScrollTextView(Context context) {
        this(context, null);
    }

    public AutoScrollTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public AutoScrollTextView(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
    }

    @Override
    protected boolean getDefaultEditable() {
        return false;
    }

    @Override
    protected MovementMethod getDefaultMovementMethod() {
        return new CursorScrollingMovementMethod();
    }

    @Override
    public void setText(CharSequence text, BufferType type) {
        super.setText(text, type);
        scrollToEnd();
    }

    @Override
    public void append(CharSequence text, int start, int end) {
        super.append(text, start, end);
        scrollToEnd();
    }

    public void scrollToEnd() {
        Editable editable = getText();
        Selection.setSelection(editable, Objects.requireNonNull(editable).length());
    }

    @Override
    public void onInitializeAccessibilityEvent(AccessibilityEvent event) {
        super.onInitializeAccessibilityEvent(event);
        event.setClassName(AutoScrollTextView.class.getName());
    }

    /**
     * Moves cursor when scrolled so it doesn't auto-scroll on configuration changes.
     */
    private static class CursorScrollingMovementMethod extends ScrollingMovementMethod {

        @Override
        public boolean onTouchEvent(TextView widget, Spannable buffer, MotionEvent event) {
            widget.moveCursorToVisibleOffset();
            return super.onTouchEvent(widget, buffer, event);
        }
    }
}
