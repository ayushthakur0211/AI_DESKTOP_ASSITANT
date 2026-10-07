import speedtest


def run_speed_test():
    st = speedtest.Speedtest()

    st.get_best_server()

    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping

    return {
        "Download Speed": f"{download:.2f} Mbps",
        "Upload Speed": f"{upload:.2f} Mbps",
        "Ping": f"{ping:.2f} ms"
    }