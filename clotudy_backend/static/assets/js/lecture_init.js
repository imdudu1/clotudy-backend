// Split.js layout
Split(['#left-side-panel', '#mid-side-panel', '#right-side-panel'], {
    elementStyle: (dimension, size, gutterSize) => ({
        'flex-basis': `calc(${size}% - ${gutterSize}px)`,
    }),
    gutterStyle: (dimension, gutterSize) => ({
        'flex-basis': `${gutterSize}px`,
    }),
    onDrag: () => {
    },
    onDragEnd: () => {
    },

    gutterSize: 24,
    minSize: [0, 0, 0],
});

Split(['#ppt-viewer-wrap', '#live-qna-chat-wrap'], {
    elementStyle: (dimension, size, gutterSize) => ({
        'flex-basis': `calc(${size}% - ${gutterSize}px)`,
    }),
    gutterStyle: (dimension, gutterSize) => ({
        'flex-basis': `${gutterSize}px`,
    }),

    gutterSize: 14,
    direction: 'vertical',
    cursor: 'row-resize',
    minSize: [0, 0],
});

Split(['#user-notepad-wrap', '#user-notepad-preview-wrap'], {
    elementStyle: (dimension, size, gutterSize) => ({
        'flex-basis': `calc(${size}% - ${gutterSize}px)`,
    }),
    gutterStyle: (dimension, gutterSize) => ({
        'flex-basis': `${gutterSize}px`,
    }),

    gutterSize: 14,
    direction: 'vertical',
    cursor: 'row-resize',
    minSize: [0, 0],
});


// Initialize Quill editor
const quill = new Quill('#user-notepad-content', {
    theme: 'snow'
});
