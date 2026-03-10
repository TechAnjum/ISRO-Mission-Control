from backend import create_app

app = create_app()

if __name__ == '__main__':
    print("""
  ╔══════════════════════════════════════════════╗
  ║     🚀  ISRO MISSION CONTROL DASHBOARD       ║
  ║     Running at: http://127.0.0.1:5000        ║
  ╚══════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
