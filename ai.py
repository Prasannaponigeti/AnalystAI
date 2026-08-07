def generate_business_insights(prompt, df=None):
    try:
        # Your Gemini code (keep it if quota works later)
        from google import genai
        import os

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        # 🔥 FALLBACK (THIS SAVES YOUR PROJECT)
        if df is not None:
            total_sales = df["Total"].sum()
            avg_sales = df["Total"].mean()
            top_city = df.groupby("City")["Total"].sum().idxmax()

            return f"""
🔹 Key Insights:
- Total Sales: {total_sales:.2f}
- Average Sales: {avg_sales:.2f}
- Top Performing City: {top_city}

🔹 Recommendations:
- Focus more on {top_city}
- Improve low-performing regions

🔹 Risks:
- Sales dependency on one region

🔹 Opportunities:
- Expand high-performing products
"""
        else:
            return "⚠️ AI service unavailable. Showing basic insights only."