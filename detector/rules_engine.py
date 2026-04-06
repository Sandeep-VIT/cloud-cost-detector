def check_idle_compute(cpu_df, threshold=5.0):
    """Flag EC2 instance as idle if avg CPU < threshold%."""
    avg_cpu = cpu_df['Average'].mean()
    if avg_cpu < threshold:
        return {
            'leak_type': 'IDLE_COMPUTE',
            'severity': 'HIGH',
            'avg_cpu': round(avg_cpu, 2),
            'recommendation': 'Stop or terminate this instance.'
        }
    return None  # No leak detected
