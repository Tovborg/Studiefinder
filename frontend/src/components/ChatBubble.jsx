export default function ChatBubble({ role, content, user }) {
  const isUser = role === 'user'

  return (
    <div className={`flex items-start gap-2.5 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <img
          className="w-8 h-8 rounded-full"
          src="https://custom.typingmind.com/assets/models/deepseek.png"
          alt="AI avatar"
        />
      )}
      <div
        className={`flex flex-col max-w-[80%] p-4 rounded-2xl shadow-sm ${
          isUser
            ? 'bg-indigo-100 text-right rounded-br-none ml-auto'
            : 'bg-gray-100 text-left rounded-bl-none'
        }`}
      >
        <p className="text-sm text-gray-900 whitespace-pre-wrap">{content}</p>
      </div>
      {isUser && (
        <img
          className="w-8 h-8 rounded-full"
          src={user.picture}
          alt="User avatar"
        />
      )}
    </div>
  )
}