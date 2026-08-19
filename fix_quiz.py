import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''                if submitted:
                    for i, q in enumerate(questions):
                        options = q.get('options', [])
                        correct_answer = q.get('answer')
                        
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

# Find the specific block to replace
pattern = r'                if submitted:\n                    for i, q in enumerate\(questions\):\n                        options = q\.get\(\'options\', \[\]\)\n                        correct_idx = q\.get\(\'correct_index\', 0\)\n                        correct_answer = options\[correct_idx\] if correct_idx < len\(options\) else None\n                        \n                        user_answer = st\.session_state\.get\(f"q_\{i\}"\)\n                        st\.session_state\.quiz_answers\[i\] = user_answer\n                        \n                        if user_answer == correct_answer:\n                            score \+= 1\n                            st\.success\(f"\*\*Q\{i\+1\}: Correct!\*\* \{q\.get\(\'explanation\', \'\'\)\}"\)\n                        else:\n                            st\.error\(f"\*\*Q\{i\+1\}: Incorrect\.\*\* Correct answer was: \{correct_answer\}\. \{q\.get\(\'explanation\', \'\'\)\}"\)\n                            \n                    st\.metric\("Final Score", f"\{score\} / \{len\(questions\)\}"\)\n                    if score == len\(questions\):\n                        st\.balloons\(\)'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
