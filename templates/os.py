import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.response_time = 0

class CPUScheduler:
    def __init__(self):
        self.queue = []
        self.clock = 0

    def add_process(self, process):
        self.queue.append(process)

    def fcfs(self):
        self.queue.sort(key=lambda x: x.arrival_time)
        for process in self.queue:
            if process.arrival_time > self.clock:
                self.clock = process.arrival_time
            process.waiting_time = self.clock - process.arrival_time
            process.response_time = process.waiting_time
            self.clock += process.burst_time
            process.completion_time = self.clock
            process.turnaround_time = process.completion_time - process.arrival_time

    def sjf(self):
        self.queue.sort(key=lambda x: (x.arrival_time, x.burst_time))
        for process in self.queue:
            if process.arrival_time > self.clock:
                self.clock = process.arrival_time
            process.waiting_time = self.clock - process.arrival_time
            process.response_time = process.waiting_time
            self.clock += process.burst_time
            process.completion_time = self.clock
            process.turnaround_time = process.completion_time - process.arrival_time

    def rr(self, quantum):
        queue = self.queue.copy()
        remaining_burst = [process.burst_time for process in queue]
        while any(remaining_burst):
            for i, process in enumerate(queue):
                if process.arrival_time <= self.clock and remaining_burst[i] > 0:
                    execute_time = min(quantum, remaining_burst[i])
                    remaining_burst[i] -= execute_time
                    self.clock += execute_time
                    if remaining_burst[i] == 0:
                        process.completion_time = self.clock
                        process.turnaround_time = process.completion_time - process.arrival_time
                        process.waiting_time = process.turnaround_time - process.burst_time
                    else:
                        process.waiting_time = self.clock - process.arrival_time - process.burst_time
                    process.response_time = process.waiting_time if process.response_time == 0 else process.response_time
                    queue.append(process)

    def display_results(self):
        result_text = ""
        total_waiting_time = sum(process.waiting_time for process in self.queue)
        total_turnaround_time = sum(process.turnaround_time for process in self.queue)
        total_response_time = sum(process.response_time for process in self.queue)
        avg_waiting_time = total_waiting_time / len(self.queue)
        avg_turnaround_time = total_turnaround_time / len(self.queue)
        avg_response_time = total_response_time / len(self.queue)
        
        result_text += "+" + "-"*53 + "+\n"
        result_text += "| PID | Arrival Time | Burst Time | CT  | TAT | WT  | RT  |\n"
        result_text += "+" + "-"*53 + "+\n"
        for process in self.queue:
            result_text += f"| {process.pid:3} | {process.arrival_time:12} | {process.burst_time:10} | {process.completion_time:3} | {process.turnaround_time:3} | {process.waiting_time:3} | {process.response_time:3} |\n"
        result_text += "+" + "-"*53 + "+\n"
        result_text += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        result_text += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        result_text += f"Average Response Time: {avg_response_time:.2f}\n"

        # Generate Gantt Chart
        gantt_chart = ""
        prev_end_time = 0
        for process in self.queue:
            if len(gantt_chart) + process.burst_time + 4 <= 60:
                gantt_chart += "+" + "-" * process.burst_time + "+"
                prev_end_time = process.arrival_time + process.burst_time
            else:
                break
        gantt_chart = "+" + "-" * (prev_end_time - 1) + "+\n" + gantt_chart
        
        result_text += "\nGantt Chart:\n"
        result_text += gantt_chart + "\n"
        
        return result_text


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("CPU Scheduler")
        self.master.geometry("1000x800")
        self.master.resizable(False, False)

        self.content_frame = tk.Frame(master, bg="#f0f0f0")
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        self.title_label = tk.Label(self.content_frame, text="CPU Scheduler", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        self.label1 = tk.Label(self.content_frame, text="Process ID:", bg="#f0f0f0")
        self.label1.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.label2 = tk.Label(self.content_frame, text="Arrival Time:", bg="#f0f0f0")
        self.label2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.label3 = tk.Label(self.content_frame, text="Burst Time:", bg="#f0f0f0")
        self.label3.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.pid_entry = tk.Entry(self.content_frame)
        self.pid_entry.grid(row=1, column=1, padx=10, pady=5)
        self.arrival_entry = tk.Entry(self.content_frame)
        self.arrival_entry.grid(row=2, column=1, padx=10, pady=5)
        self.burst_entry = tk.Entry(self.content_frame)
        self.burst_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.content_frame, text="Add Process", command=self.add_process, bg="#4CAF50", fg="white")
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.algorithm_label = tk.Label(self.content_frame, text="Choose Algorithm:", bg="#f0f0f0")
        self.algorithm_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.algorithm_var = tk.StringVar(master)
        self.algorithm_var.set("FCFS")
        self.algorithm_menu = ttk.Combobox(self.content_frame, textvariable=self.algorithm_var, values=["FCFS", "SJF", "RR"])
        self.algorithm_menu.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.run_button = tk.Button(self.content_frame, text="Run Scheduler", command=self.run_scheduler, bg="#008CBA", fg="white")
        self.run_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(self.content_frame, height=10, width=60, bg="white", fg="black")
        self.result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=(0, 20))

        self.scheduler = CPUScheduler()

    def add_process(self):
        pid = int(self.pid_entry.get())
        arrival_time = int(self.arrival_entry.get())
        burst_time = int(self.burst_entry.get())
        process = Process(pid, arrival_time, burst_time)
        self.scheduler.add_process(process)
        self.pid_entry.delete(0, 'end')
        self.arrival_entry.delete(0, 'end')
        self.burst_entry.delete(0, 'end')

    def run_scheduler(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "FCFS":
            self.scheduler.fcfs()
        elif algorithm == "SJF":
            self.scheduler.sjf()
        elif algorithm == "RR":
            quantum = simpledialog.askinteger("Quantum", "Enter Quantum for Round Robin:")
            if quantum is not None:
                self.scheduler.rr(quantum)
            else:
                return
        result = self.scheduler.display_results()
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
