from portfolio_ai_resume import create_app

app = create_app()

if __name__ == "__main__":
    # For local dev. Use gunicorn/uvicorn in prod.
    app.run(host="0.0.0.0", port=5000, debug=True)