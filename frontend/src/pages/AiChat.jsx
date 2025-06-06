// src/pages/AiChat.jsx
import { useParams } from 'react-router-dom'
import Header from '../components/Header'
import { useEffect, useState, useRef } from 'react'
import ChatBubble from '../components/ChatBubble.jsx'
import { useAuth } from '../context/AuthContext'
import { useLocation, useNavigate } from 'react-router-dom'
import TypingBubble from '../components/TypingBubble.jsx'


function ChatInput({ input, setInput, handleSubmit }) {
    return (
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl bg-white/70 backdrop-blur-sm shadow-lg rounded-xl px-2 py-2 flex items-center gap-2 mx-auto border border-gray-200"
      >
        <input
          type="text"
          placeholder="Stil et spørgsmål til AI..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-white/60 backdrop-blur-md text-sm rounded-md px-4 py-2 text-gray-800 placeholder-gray-400 border border-gray-300 focus:border-indigo-400 focus:outline-none focus:ring-0 transition"
        />
        <button
          type="submit"
          className="text-indigo-600 font-semibold hover:text-indigo-800 transition px-3"
        >
          Send
        </button>
      </form>
    )
  }

export default function AiChat() {
  const { studyName } = useParams()
  const { user } = useAuth()
  const [hasStartedChat, setHasStartedChat] = useState(false)
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [messages, setMessages] = useState([])
  const messagesEndRef = useRef(null)
  // Hent prompt fra state
  const location = useLocation()
  const prompt = location.state?.prompt // safe access

  useEffect(() => {
    document.title = `AI Chat - ${studyName}`
    if (prompt) {
    console.log("📬 Prompt fra tidligere:", prompt)
    }
  }, [studyName, prompt])

  useEffect(() => {
    if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  useEffect(() => {
    document.title = `AI Chat - ${studyName}`
  }, [studyName])

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/chat-history?user_id=${user.id}&uddannelse_name=${studyName}`)
        if (!response.ok) {
          throw new Error("Failed to fetch chat history")
        }
  
        const data = await response.json()
        if (data.length > 0) {
          // Populate messages state with chat history
          const chatMessages = data.flatMap((entry) => [
            { role: "user", content: entry.user_message },
            { role: "assistant", content: entry.assistant_message },
          ])
  
          setMessages(chatMessages)
          setHasStartedChat(true)
  
          // Scroll to the bottom to view the latest messages
          if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
          }
        } else {
          setHasStartedChat(false)
        }
      } catch (error) {
        console.error("Error fetching chat history:", error)
        setHasStartedChat(false)
      }
    }
  
    fetchChatHistory()
  }, [studyName, user.id])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (input.trim() === "") return
  
    setHasStartedChat(true)
    setMessages(prev => [...prev, { role: 'user', content: input }])
    setIsTyping(true) // Simulerer AI-typing
    try {
        const res = await fetch("http://localhost:8000/api/ai-chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            original_prompt: prompt, // fra location.state
            study_name: decodeURIComponent(studyName),
            user_id: user.id,
            question: input,
          }),
        })
    
        const data = await res.json()
        console.log("🤖 AI svar:", data.reply)
    
        setMessages(prev => [...prev, { role: 'assistant', content: data.reply }])
      } catch (err) {
        console.error("Fejl under API-kald:", err)
      } finally {
        setIsTyping(false)
        setInput("") // Tøm inputfeltet
      }
    
      setInput("")
  }
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f8f9fc] via-[#f4f2fa] to-[#fefefe] flex flex-col">
      <Header />
      <div className="w-full max-w-3xl text-center mt-20 mb-0 ml-7">
        <div className="flex justify-start">
          <button
            onClick={() => navigate(-1)}
            className="text-sm text-gray-500 hover:text-gray-800 bg-white/80 backdrop-blur-sm border border-gray-200 px-3 py-1 rounded-full shadow-sm transition"
          >
            ← Tilbage
          </button>
        </div>
      </div>
      <main className="flex-1 flex flex-col items-center justify-center px-4 relative">
        
        {!hasStartedChat && (
            <div className="w-full max-w-3xl text-center">
             {/* Tilbage-knap længere oppe, men stadig venstrestillet */}
         
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-semibold text-gray-900 mb-4">
              Hej, hvad vil du gerne vide om{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-600">
                {decodeURIComponent(studyName)}
              </span>?
            </h1>
            <p className="text-gray-600 mb-8 max-w-xl mx-auto">
              Du kan spørge mig om uddannelsens faglige indhold, adgangskrav, karriereveje og hvorfor vi tror den matcher dig.
            </p>

            <ChatInput input={input} setInput={setInput} handleSubmit={handleSubmit} />

            <div className="mt-6 flex flex-wrap gap-2 justify-center">
              {["Hvad lærer man?", "Hvad kan man blive?", "Hvorfor passer den til mig?", "Vis lignende uddannelser"].map((text) => (
                <button
                  key={text}
                  onClick={() => {
                    setInput(text)
                    setHasStartedChat(true)
                  }}
                  className="px-3 py-1.5 rounded-full text-sm bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
                >
                  {text}
                </button>
              ))}
            </div>
          </div>
        )}

        {hasStartedChat && (
          <div className="w-full max-w-3xl flex-1 flex flex-col gap-4 px-4 py-8 overflow-y-auto">
            <p className="text-sm mb-3 text-gray-400 text-center">🧠 Klar til at besvare dine spørgsmål...</p>
            {messages.map((msg, idx) => (
              <ChatBubble key={idx} role={msg.role} content={msg.content} user={user} />
            ))}
            {isTyping && <TypingBubble />}  {/* 👈 bubble vises her */}
            <div ref={messagesEndRef} />
          </div>
        )}

      </main>

      {/* Input field fast i bunden når chat er aktiv */}
      {hasStartedChat && (
        <div className="sticky bottom-4 w-full flex justify-center px-4">
            <div className="bg-white/80 backdrop-blur-lg rounded-xl shadow-lg border border-gray-200 w-full max-w-2xl">
            <ChatInput input={input} setInput={setInput} handleSubmit={handleSubmit} />
            </div>
        </div>
        )}
    </div>
  )
}
