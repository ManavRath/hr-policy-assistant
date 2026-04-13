from rag import generate_answer

# Simulate a multi-turn conversation with explicit history
chat_history = []

q1 = "What is the leave policy?"
a1 = generate_answer(q1, chat_history=chat_history)
chat_history.append(f"User: {q1}")
chat_history.append(f"Assistant: {a1}")
print("Q:", q1)
print("A:", a1)
print()

q2 = "How many leaves can I carry forward?"
a2 = generate_answer(q2, chat_history=chat_history)
chat_history.append(f"User: {q2}")
chat_history.append(f"Assistant: {a2}")
print("Q:", q2)
print("A:", a2)