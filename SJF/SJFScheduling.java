import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Process {
    int pid;
    int arrivalTime;
    int burstTime;
    int priority;
    int waitingTime;
    int turnaroundTime;

    public Process(int pid, int arrivalTime, int burstTime, int priority) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.priority = priority;
        this.waitingTime = 0;
        this.turnaroundTime = 0;
    }
}

public class SJFScheduling {

    public static List<Process> sjfScheduling(List<Process> processes) {
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
        List<Process> completed = new ArrayList<>();
        List<Process> readyQueue = new ArrayList<>();
        int time = 0;

        while (completed.size() < processes.size()) {
            for (Process process : processes) {
                if (!completed.contains(process) && !readyQueue.contains(process) && process.arrivalTime <= time) {
                    readyQueue.add(process);
                }
            }

            if (!readyQueue.isEmpty()) {
                readyQueue.sort(Comparator.comparingInt(p -> p.burstTime));
                Process currentProcess = readyQueue.remove(0);

                currentProcess.waitingTime = time - currentProcess.arrivalTime;
                time += currentProcess.burstTime;
                currentProcess.turnaroundTime = time - currentProcess.arrivalTime;
                completed.add(currentProcess);
            } else {
                time++;
            }
        }

        return completed;
    }

    public static void calculateAvgTimes(List<Process> processes) {
        int totalWaitingTime = 0;
        int totalTurnaroundTime = 0;

        for (Process process : processes) {
            totalWaitingTime += process.waitingTime;
            totalTurnaroundTime += process.turnaroundTime;
        }

        double avgWaitingTime = (double) totalWaitingTime / processes.size();
        double avgTurnaroundTime = (double) totalTurnaroundTime / processes.size();

        System.out.printf("\nAverage Waiting Time: %.2f\n", avgWaitingTime);
        System.out.printf("Average Turnaround Time: %.2f\n", avgTurnaroundTime);
    }

    public static void main(String[] args) {
        List<Process> processList = new ArrayList<>();
        processList.add(new Process(1, 0, 8, 3));
        processList.add(new Process(2, 1, 4, 1));
        processList.add(new Process(3, 2, 9, 4));
        processList.add(new Process(4, 3, 5, 2));
        processList.add(new Process(5, 4, 2, 5));

        List<Process> completedProcesses = sjfScheduling(processList);

        System.out.println("\nSJF Scheduling Results:");
        System.out.println("Process\tArrival\tBurst\tPriority\tWaiting\tTurnaround");
        for (Process process : completedProcesses) {
            System.out.printf("P%d\t%d\t%d\t%d\t%d\t%d\n",
                    process.pid,
                    process.arrivalTime,
                    process.burstTime,
                    process.priority,
                    process.waitingTime,
                    process.turnaroundTime);
        }

        calculateAvgTimes(completedProcesses);
    }
}
