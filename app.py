import streamlit as st
import graphviz

class AgonBot:
    def __init__(self):
        self.discussion_history = []
        self.fact_database = {
            "기후 변화는 사실이다.": True,
            "지구는 평평하다.": False,
        }
        self.cot = []

    def moderate_input(self, input_text):
        inappropriate_phrases = {
            "헛소리": "다른 의견이 있을 경우 논리적으로 설명해 주세요.",
            "멍청이": "상대방을 존중하는 표현을 사용해 주세요."
        }
        for phrase, replacement in inappropriate_phrases.items():
            if phrase in input_text:
                return replacement
        return input_text

    def verify_fact(self, input_text):
        for fact, validity in self.fact_database.items():
            if fact in input_text:
                return f"사실 검증 결과: '{fact}'는 {validity}로 확인되었습니다."
        return "사실 검증 결과: 관련된 정보가 데이터베이스에 없습니다."

    def add_to_cot(self, participant, statement):
        self.cot.append({"participant": participant, "statement": statement})
        return self.cot

    def summarize_discussion(self):
        summary = []
        for entry in self.cot:
            summary.append(f"{entry['participant']}의 주장: {entry['statement']}")
        return "\n".join(summary)

st.title("아곤봇: 아고니즘 정치 지원 AI")
st.write("이 앱은 참여자 간의 논의를 중재하고 사실 검증을 제공합니다.")

st.header("참여자 발언 입력")
user_input = st.text_area("발언을 입력하세요:")
participant = st.text_input("참여자 이름:", "익명")

if st.button("처리하기"):
    if user_input:
        agonbot = AgonBot()
        moderated_input = agonbot.moderate_input(user_input)
        fact_check = agonbot.verify_fact(user_input)
        cot = agonbot.add_to_cot(participant, user_input)

        st.subheader("중재된 발언")
        st.write(moderated_input)

        st.subheader("사실 검증 결과")
        st.write(fact_check)

        st.subheader("현재 논의 구조")
        st.write(agonbot.summarize_discussion())

        st.subheader("논의 흐름 시각화")
        dot = graphviz.Digraph()
        for entry in cot:
            dot.node(entry['participant'], entry['participant'])
            dot.edge(entry['participant'], entry['statement'])
        st.graphviz_chart(dot)
    else:
        st.warning("발언을 입력하세요!")
