import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

# -------- GLOBALS --------
alloc_entries = []
max_entries = []
avail_entries = []
process_labels = []

# -------- GENERATE INPUT TABLE --------
def generate_fields():
    global alloc_entries, max_entries, avail_entries, process_labels

    for widget in table_frame.winfo_children():
        widget.destroy()

    alloc_entries.clear()
    max_entries.clear()
    avail_entries.clear()
    process_labels.clear()

    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    tk.Label(table_frame, text="Allocation", font=("Arial", 10, "bold")).grid(row=0, column=1, columnspan=m)
    tk.Label(table_frame, text="Max", font=("Arial", 10, "bold")).grid(row=0, column=m+2, columnspan=m)

    for i in range(n):
        tk.Label(table_frame, text=f"P{i}").grid(row=i+1, column=0)
        process_labels.append(f"P{i}")

        alloc_row = []
        max_row = []

        for j in range(m):
            e = tk.Entry(table_frame, width=5)
            e.insert(0, "0")
            e.grid(row=i+1, column=j+1)
            alloc_row.append(e)

        for j in range(m):
            e = tk.Entry(table_frame, width=5)
            e.insert(0, "0")
            e.grid(row=i+1, column=j+m+2)
            max_row.append(e)

        alloc_entries.append(alloc_row)
        max_entries.append(max_row)

    # Available row
    tk.Label(root, text="Available Resources").pack()
    avail_frame = tk.Frame(root)
    avail_frame.pack()

    for j in range(m):
        e = tk.Entry(avail_frame, width=5)
        e.insert(0, "0")
        e.pack(side="left", padx=5)
        avail_entries.append(e)

# -------- WAIT-FOR GRAPH --------
def show_graph(processes, allocation, need):
    G = nx.DiGraph()

    n = len(processes)
    m = len(allocation[0])

    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(m):
                    if need[i][k] > 0 and allocation[j][k] > 0:
                        G.add_edge(processes[i], processes[j])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue')
    plt.title("Wait-For Graph")
    plt.show()

# -------- ANIMATION --------
def animate(sequence):
    output_text.delete("1.0", tk.END)
    for p in sequence:
        output_text.insert(tk.END, f"Executing {p}...\n")
        root.update()
        root.after(700)
    output_text.insert(tk.END, "Execution Completed\n")

# -------- MAIN LOGIC --------
def check_safe():
    try:
        n = len(alloc_entries)
        m = len(avail_entries)
        processes = process_labels

        allocation = [[int(alloc_entries[i][j].get()) for j in range(m)] for i in range(n)]
        max_need = [[int(max_entries[i][j].get()) for j in range(m)] for i in range(n)]
        available = [int(avail_entries[j].get()) for j in range(m)]

        need = [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

        finish = [False] * n
        safe_seq = []
        work = available.copy()

        while len(safe_seq) < n:
            allocated = False
            for i in range(n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                    for j in range(m):
                        work[j] += allocation[i][j]
                    safe_seq.append(processes[i])
                    finish[i] = True
                    allocated = True

            if not allocated:
                result_label.config(text="❌ DEADLOCK DETECTED", fg="red")
                show_graph(processes, allocation, need)
                return

        result_label.config(text="✅ SAFE STATE", fg="green")
        animate(safe_seq)
        show_graph(processes, allocation, need)

    except:
        messagebox.showerror("Error", "Invalid Input")

# -------- GUI --------
root = tk.Tk()
root.title("Deadlock Simulator - Advanced")
root.geometry("900x650")

tk.Label(root, text="Deadlock Detection Simulator", font=("Arial", 16, "bold")).pack(pady=10)

# Input n, m
tk.Label(root, text="Number of Processes").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Label(root, text="Number of Resources").pack()
entry_m = tk.Entry(root)
entry_m.pack()

tk.Button(root, text="Generate Table", command=generate_fields, bg="blue", fg="white").pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack()

tk.Button(root, text="Check System State", command=check_safe, bg="green", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

output_text = tk.Text(root, height=10, width=60)
output_text.pack(pady=10)

root.mainloop()