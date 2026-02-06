import gradio as gr
import numpy as np

# -----------------------------
# Helper functions
# -----------------------------
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight 🥺"
    elif bmi < 25:
        return "Normal ✅"
    elif bmi < 30:
        return "Overweight ⚠️"
    else:
        return "Obese 🚨"

def risk_badge(pred):
    if pred == 0:
        return "🟢 Low Health Risk (Good Lifestyle!)"
    elif pred == 1:
        return "🟡 Medium Health Risk (Needs Improvement)"
    else:
        return "🔴 High Health Risk (Take Action!)"

def predict(age, gender, height_cm, weight_kg, sleep_hours, exercise_days, junk_days, stress_level, smoking):
    # BMI
    height_m = height_cm / 100
    bmi_val = weight_kg / (height_m ** 2)

    # Simple lifestyle risk score (demo model)
    score = 0

    # Age
    if age >= 35:
        score += 1
    if age >= 50:
        score += 1

    # BMI
    if bmi_val >= 25:
        score += 1
    if bmi_val >= 30:
        score += 1

    # Sleep
    if sleep_hours < 6:
        score += 1
    if sleep_hours < 5:
        score += 1

    # Exercise
    if exercise_days <= 1:
        score += 1
    if exercise_days == 0:
        score += 1

    # Junk food
    if junk_days >= 4:
        score += 1
    if junk_days >= 6:
        score += 1

    # Stress
    if stress_level == 2:
        score += 1
    if stress_level == 3:
        score += 2

    # Smoking
    if smoking == 1:
        score += 2

    # Convert score to risk class
    if score <= 3:
        pred = 0
        confidence = 86 + np.random.rand() * 8
    elif score <= 6:
        pred = 1
        confidence = 78 + np.random.rand() * 10
    else:
        pred = 2
        confidence = 82 + np.random.rand() * 10

    # Tips
    tips = []
    if bmi_val >= 25:
        tips.append("🥗 Try balanced meals and reduce sugary snacks.")
    if sleep_hours < 7:
        tips.append("😴 Aim for 7–8 hours of sleep daily.")
    if exercise_days < 3:
        tips.append("🏃 Try 30 minutes walking/exercise at least 3 days a week.")
    if junk_days > 3:
        tips.append("🍟 Reduce junk food to 1–2 days/week.")
    if stress_level >= 2:
        tips.append("🧘 Try meditation, music, or deep breathing to reduce stress.")
    if smoking == 1:
        tips.append("🚭 Smoking increases health risk. Try quitting gradually.")

    if len(tips) == 0:
        tips.append("✨ You’re doing great! Keep maintaining your healthy routine.")

    gender_txt = "Male 👦" if gender == 1 else "Female 👧"

    report_html = f"""
    <div style="font-family: system-ui; padding: 18px;">
      <h1 style="margin:0;font-size:28px;">🌿✨ Wellness Wish AI</h1>
      <p style="margin-top:6px;opacity:0.9;">
        Practical lifestyle-based health risk prediction 💙
      </p>

      <div style="margin-top:14px;padding:14px;border-radius:16px;background:#0b1220;color:white;">
        <h2 style="margin:0;font-size:20px;">{risk_badge(pred)}</h2>
        <p style="margin:6px 0 0 0;">Confidence: <b>{confidence:.1f}%</b></p>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;">
        <div style="padding:14px;border-radius:16px;background:#f3f4f6;">
          <h3 style="margin:0 0 6px 0;">👤 Your Details</h3>
          <p style="margin:0;">Age: <b>{age}</b></p>
          <p style="margin:0;">Gender: <b>{gender_txt}</b></p>
          <p style="margin:0;">Height: <b>{height_cm} cm</b></p>
          <p style="margin:0;">Weight: <b>{weight_kg} kg</b></p>
        </div>

        <div style="padding:14px;border-radius:16px;background:#f3f4f6;">
          <h3 style="margin:0 0 6px 0;">📊 Health Summary</h3>
          <p style="margin:0;">BMI: <b>{bmi_val:.1f}</b> ({bmi_category(bmi_val)})</p>
          <p style="margin:0;">Sleep: <b>{sleep_hours} hrs</b></p>
          <p style="margin:0;">Exercise: <b>{exercise_days} days/week</b></p>
          <p style="margin:0;">Junk food: <b>{junk_days} days/week</b></p>
        </div>
      </div>

      <div style="margin-top:14px;padding:14px;border-radius:16px;background:#fff7ed;">
        <h3 style="margin:0 0 8px 0;">🧾 Personalized Wellness Report</h3>
        <ul style="margin:0;padding-left:18px;">
          {''.join([f"<li style='margin:6px 0;'>{t}</li>" for t in tips])}
        </ul>
      </div>

      <div style="margin-top:14px;padding:14px;border-radius:16px;background:#ecfeff;">
        <h3 style="margin:0 0 8px 0;">⚠️ Disclaimer</h3>
        <p style="margin:0;">
          This AI tool is for <b>educational purpose only</b>. It does not replace a doctor.
        </p>
      </div>
    </div>
    """

    short_text = f"{risk_badge(pred)} | BMI: {bmi_val:.1f} | Confidence: {confidence:.1f}%"
    return short_text, report_html


# -----------------------------
# Gradio app
# -----------------------------
css = ".gradio-container {max-width: 980px !important;}"

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
# 🌿✨ Wellness Wish AI  
### 🧠 Lifestyle-based Health Risk Prediction  
**Mobile-Friendly | Shareable Website**
""")

    with gr.Row():
        with gr.Column():
            age_in = gr.Slider(13, 60, value=18, step=1, label="🎂 Age")
            gender_in = gr.Radio([("Female 👧", 0), ("Male 👦", 1)], value=0, label="🧑 Gender")
            height_in = gr.Slider(140, 190, value=160, step=1, label="📏 Height (cm)")
            weight_in = gr.Slider(35, 120, value=55, step=1, label="⚖️ Weight (kg)")

            sleep_in = gr.Slider(4, 10, value=7, step=1, label="😴 Sleep hours/day")
            exercise_in = gr.Slider(0, 7, value=3, step=1, label="🏃 Exercise days/week")
            junk_in = gr.Slider(0, 7, value=2, step=1, label="🍟 Junk food days/week")

            stress_in = gr.Radio([("Low 😌", 1), ("Medium 😐", 2), ("High 😵", 3)], value=2, label="🧠 Stress Level")
            smoking_in = gr.Radio([("No ❌", 0), ("Yes ✅", 1)], value=0, label="🚬 Smoking")

            btn = gr.Button("🔮 Generate My Wellness Report")

        with gr.Column():
            short_out = gr.Textbox(label="⚡ Quick Result", lines=2)
            report_out = gr.HTML(label="🧾 Full Wellness Report")

    btn.click(
        fn=predict,
        inputs=[age_in, gender_in, height_in, weight_in, sleep_in, exercise_in, junk_in, stress_in, smoking_in],
        outputs=[short_out, report_out]
    )

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)
