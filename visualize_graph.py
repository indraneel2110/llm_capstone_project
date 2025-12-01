from main import app

print("Generating graph image...")
image_data = app.get_graph().draw_mermaid_png()
    
with open("graph_architecture.png", "wb") as f:
        f.write(image_data)

