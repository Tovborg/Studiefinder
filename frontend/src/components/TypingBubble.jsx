// src/components/TypingBubble.jsx
export default function TypingBubble() {
    return (
      <div className="flex items-center gap-2.5">
        <img
          className="w-8 h-8 rounded-full"
          src="https://custom.typingmind.com/assets/models/deepseek.png"
          alt="AI avatar"
        />
        <div className="flex items-center gap-1 px-4 py-3 rounded-2xl bg-gray-100 shadow-sm">
          <span className="h-2 w-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0.1s]"></span>
          <span className="h-2 w-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
          <span className="h-2 w-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0.3s]"></span>
        </div>
      </div>
    )
  }