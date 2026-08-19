import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

quiz_replacement = '''            if not questions:
                st.error("Quiz data format was invalid.")
            else:
                score = 0
                with st.form("quiz_form"):
                    for i, q in enumerate(questions):
                        st.subheader(f"Q{i+1}: {q.get('question', 'Question text missing')}")
                        
                        options = q.get('options', [])
                        selected = st.radio(
                            "Select an answer:",
                            options,
                            key=f"q_{i}",
                            index=None
                        )
                        
                    submitted = st.form_submit_button("Submit Answers")
                    
                if submitted:
                    for i, q in enumerate(questions):
                        options = q.get('options', [])
                        correct_idx = q.get('correct_index', 0)
                        correct_answer = options[correct_idx] if correct_idx < len(options) else None
                        
                        user_answer = st.session_state.get(f"q_{i}")
                        st.session_state.quiz_answers[i] = user_answer
                        
                        if user_answer == correct_answer:
                            score += 1
                            st.success(f"**Q{i+1}: Correct!** {q.get('explanation', '')}")
                        else:
                            st.error(f"**Q{i+1}: Incorrect.** Correct answer was: {correct_answer}. {q.get('explanation', '')}")
                            
                    st.metric("Final Score", f"{score} / {len(questions)}")
                    if score == len(questions):
                        st.balloons()
'''

content = re.sub(r'            if not questions:.*?st\.balloons\(\)', quiz_replacement, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
