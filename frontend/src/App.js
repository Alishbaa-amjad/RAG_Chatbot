import { useState } from "react";
import ReactMarkdown from 'react-markdown';

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    const userMessage = question;
    setMessages(prev => [...prev, { type: "user", text: userMessage }]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, {
        type: "bot",
        text: data.answer,
        sources: data.sources
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: "bot",
        text: "Connection error. Please try again.",
        sources: []
      }]);
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "#b2dfdb",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      fontFamily: "'Segoe UI', sans-serif",
      padding: "20px"
    }}>

      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: "24px", marginTop: "16px" }}>
        <h1 style={{
          color: "#004d40",
          fontSize: "32px",
          fontWeight: "700",
          margin: "0",
          letterSpacing: "1px"
        }}>🤖 NETSOL AI Assistant</h1>
        <p style={{ color: "#00796b", fontSize: "14px", margin: "8px 0 0 0" }}>
          Powered by LangGraph + Gemini LLM
        </p>
        <div style={{
          width: "60px", height: "3px",
          background: "linear-gradient(90deg, #00897b, #4db6ac)",
          margin: "12px auto 0", borderRadius: "2px"
        }} />
      </div>

      {/* Stats Cards */}
      <div style={{
        display: "flex",
        gap: "16px",
        width: "100%",
        maxWidth: "960px",
        marginBottom: "20px",
        flexWrap: "wrap"
      }}>
        {[
          { icon: "🌍", title: "Global Reach", value: "30+ Countries" },
          { icon: "💼", title: "Experience", value: "30+ Years" },
          { icon: "⭐", title: "Success Rate", value: "100% Implementation" },
          { icon: "💰", title: "Assets Managed", value: "$500B+" }
        ].map((card, i) => (
          <div key={i} style={{
            flex: 1,
            minWidth: "150px",
            background: "#ffffff",
            border: "1.5px solid #80cbc4",
            borderRadius: "14px",
            padding: "16px",
            textAlign: "center"
          }}>
            <div style={{ fontSize: "28px" }}>{card.icon}</div>
            <div style={{
              color: "#00796b", fontSize: "11px",
              marginTop: "6px", letterSpacing: "1px", fontWeight: "600"
            }}>{card.title}</div>
            <div style={{
              color: "#004d40", fontSize: "13px",
              fontWeight: "700", marginTop: "4px"
            }}>{card.value}</div>
          </div>
        ))}
      </div>

      {/* Main Layout */}
      <div style={{
        display: "flex",
        gap: "20px",
        width: "100%",
        maxWidth: "960px",
        alignItems: "flex-start"
      }}>

        {/* Left Sidebar */}
        <div style={{
          width: "220px",
          flexShrink: 0,
          display: "flex",
          flexDirection: "column",
          gap: "12px"
        }}>
          <div style={{
            background: "#ffffff",
            border: "1.5px solid #80cbc4",
            borderRadius: "14px",
            padding: "16px"
          }}>
            <p style={{
              color: "#00796b", fontSize: "11px",
              letterSpacing: "1px", margin: "0 0 12px 0",
              fontWeight: "700"
            }}>💡 SUGGESTED QUESTIONS</p>
            {[
              "What is NETSOL?",
              "Where is NETSOL headquartered?",
              "What products does NETSOL offer?",
              "What services does NETSOL provide?",
              "When was NETSOL founded?"
            ].map((q, i) => (
              <div key={i}
                onClick={() => setQuestion(q)}
                style={{
                  color: "#004d40",
                  fontSize: "12px",
                  padding: "8px 10px",
                  marginBottom: "6px",
                  borderRadius: "8px",
                  cursor: "pointer",
                  background: "#e0f2f1",
                  border: "1px solid #b2dfdb",
                  lineHeight: "1.4"
                }}
                onMouseEnter={e => e.currentTarget.style.background = "#b2dfdb"}
                onMouseLeave={e => e.currentTarget.style.background = "#e0f2f1"}
              >
                {q}
              </div>
            ))}
          </div>

          <div style={{
            background: "#ffffff",
            border: "1.5px solid #80cbc4",
            borderRadius: "14px",
            padding: "16px"
          }}>
            <p style={{
              color: "#00796b", fontSize: "11px",
              letterSpacing: "1px", margin: "0 0 10px 0",
              fontWeight: "700"
            }}>🔗 QUICK LINKS</p>
            {[
              { label: "NETSOL Website", url: "https://netsoltech.com" },
              { label: "About NETSOL", url: "https://netsoltech.com/about-us" },
              { label: "Products", url: "https://netsoltech.com/products" },
              { label: "Services", url: "https://netsoltech.com/services" },
            ].map((link, i) => (
              <a key={i} href={link.url} target="_blank" rel="noreferrer"
                style={{
                  display: "block",
                  color: "#00796b",
                  fontSize: "12px",
                  textDecoration: "none",
                  marginBottom: "6px",
                  padding: "6px 10px",
                  borderRadius: "8px",
                  background: "#e0f2f1",
                  border: "1px solid #b2dfdb"
                }}
                onMouseEnter={e => e.currentTarget.style.background = "#b2dfdb"}
                onMouseLeave={e => e.currentTarget.style.background = "#e0f2f1"}
              >
                🔗 {link.label}
              </a>
            ))}
          </div>
        </div>

        {/* Chat Area */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "16px" }}>

          {/* Chat Window */}
          <div style={{
            background: "#ffffff",
            borderRadius: "20px",
            border: "1.5px solid #80cbc4",
            padding: "20px",
            minHeight: "420px",
            maxHeight: "420px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "16px"
          }}>
            {messages.length === 0 && (
              <div style={{
                textAlign: "center",
                color: "#80cbc4",
                marginTop: "140px",
                fontSize: "14px"
              }}>
                <div style={{ fontSize: "36px", marginBottom: "10px" }}>💬</div>
                Ask me anything about NETSOL Technologies!
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} style={{
                display: "flex",
                justifyContent: msg.type === "user" ? "flex-end" : "flex-start",
                gap: "10px",
                alignItems: "flex-start"
              }}>
                {msg.type === "bot" && (
                  <div style={{
                    width: "32px", height: "32px", borderRadius: "50%",
                    background: "#b2dfdb",
                    border: "1px solid #80cbc4",
                    display: "flex", alignItems: "center",
                    justifyContent: "center", fontSize: "16px", flexShrink: 0
                  }}>🤖</div>
                )}
                <div style={{
                  maxWidth: "75%",
                  background: msg.type === "user" ? "#00897b" : "#e0f2f1",
                  color: msg.type === "user" ? "#ffffff" : "#004d40",
                  padding: "12px 16px",
                  borderRadius: msg.type === "user"
                    ? "18px 18px 4px 18px"
                    : "18px 18px 18px 4px",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  border: msg.type === "bot" ? "1px solid #b2dfdb" : "none"
                }}>
                  {msg.type === "bot" ? (
                    <div style={{ margin: 0 }}>
                      <ReactMarkdown
                        components={{
                          p: ({children}) => <p style={{margin: '4px 0', color: '#004d40'}}>{children}</p>,
                          ul: ({children}) => <ul style={{margin: '8px 0', paddingLeft: '20px', color: '#004d40'}}>{children}</ul>,
                          ol: ({children}) => <ol style={{margin: '8px 0', paddingLeft: '20px', color: '#004d40'}}>{children}</ol>,
                          li: ({children}) => <li style={{margin: '4px 0', color: '#004d40'}}>{children}</li>,
                          strong: ({children}) => <strong style={{color: '#00695c', fontWeight: '700'}}>{children}</strong>,
                        }}
                      >
                        {msg.text}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    <p style={{ margin: 0 }}>{msg.text}</p>
                  )}

                  {msg.sources && msg.sources.length > 0 && (
                    <div style={{
                      marginTop: "10px", paddingTop: "10px",
                      borderTop: "1px solid #80cbc4"
                    }}>
                      <p style={{
                        margin: "0 0 6px 0", fontSize: "11px",
                        color: "#00796b", fontWeight: "700", letterSpacing: "1px"
                      }}>📎 SOURCES</p>
                      {msg.sources.map((s, j) => (
                        <a key={j} href={s} target="_blank" rel="noreferrer"
                          style={{
                            display: "block", color: "#00897b",
                            fontSize: "12px", textDecoration: "none", marginBottom: "3px"
                          }}>🔗 {s}</a>
                      ))}
                    </div>
                  )}
                </div>
                {msg.type === "user" && (
                  <div style={{
                    width: "32px", height: "32px", borderRadius: "50%",
                    background: "#b2dfdb",
                    border: "1px solid #80cbc4",
                    display: "flex", alignItems: "center",
                    justifyContent: "center", fontSize: "16px", flexShrink: 0
                  }}>👩</div>
                )}
              </div>
            ))}

            {loading && (
              <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                <div style={{
                  width: "32px", height: "32px", borderRadius: "50%",
                  background: "#b2dfdb",
                  border: "1px solid #80cbc4",
                  display: "flex", alignItems: "center",
                  justifyContent: "center", fontSize: "16px"
                }}>🤖</div>
                <div style={{
                  background: "#e0f2f1",
                  padding: "12px 20px", borderRadius: "18px 18px 18px 4px",
                  border: "1px solid #b2dfdb"
                }}>
                  <div style={{ display: "flex", gap: "4px" }}>
                    {[0, 1, 2].map(i => (
                      <div key={i} style={{
                        width: "8px", height: "8px", borderRadius: "50%",
                        background: "#00897b",
                        animation: "bounce 1s infinite",
                        animationDelay: `${i * 0.2}s`
                      }} />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
            <input
              style={{
                flex: 1, padding: "16px 20px", fontSize: "15px",
                background: "#ffffff",
                border: "1.5px solid #80cbc4",
                borderRadius: "50px", color: "#004d40", outline: "none",
              }}
              type="text"
              placeholder="Ask about NETSOL Technologies..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && askQuestion()}
            />
            <button
              onClick={askQuestion}
              disabled={loading}
              style={{
                padding: "16px 28px", fontSize: "15px",
                background: loading ? "#80cbc4" : "#00897b",
                color: "#ffffff", border: "none",
                borderRadius: "50px",
                cursor: loading ? "not-allowed" : "pointer",
                fontWeight: "700", whiteSpace: "nowrap"
              }}
            >
              {loading ? "..." : "Ask ✨"}
            </button>
          </div>
        </div>
      </div>

      <p style={{
        color: "#4db6ac",
        fontSize: "12px", marginTop: "20px"
      }}>
        NETSOL Chatbot — Built with React + FastAPI + LangGraph
      </p>

      <style>{`
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
        input::placeholder { color: #80cbc4; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #e0f2f1; }
        ::-webkit-scrollbar-thumb { background: #80cbc4; border-radius: 3px; }
      `}</style>
    </div>
  );
}

export default App;