from shiny import App, ui, reactive, render
import pandas as pd

# ----- UI -----
app_ui = ui.page_fluid(
    ui.tags.style("""
        /* Latar belakang halaman */
        body {
            margin: 0;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        /* Frame utama di tengah */
        .frame {
            background: #fff;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            padding: 30px;
            width: 90%;
            max-width: 500px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        /* Judul formulir */
        .frame h2 {
            margin-bottom: 20px;
            font-size: 1.8em;
            color: #333;
        }

        /* Input teks */
        .frame .shiny-input-container {
            margin-bottom: 15px;
            text-align: left;
            width: 100%;
        }

        .frame .shiny-input-container input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
        }

        /* Tombol Ya dan Tidak */
        .btn-group {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-top: 20px;
            width: 100%;
        }

        .btn-group .btn-yes,
        .btn-group .btn-no {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.3s ease;
            position: relative;
        }

        .btn-group .btn-yes {
            background: #28a745;
            color: #fff;
        }

        .btn-group .btn-no {
            background: #dc3545;
            color: #fff;
        }

        .btn-group .btn-yes:hover {
            background: #218838;
        }

        .btn-group .btn-no:hover {
            background: #c82333;
        }

        /* Indikator Bulatan Pilihan */
        .btn-group .indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            background: transparent;
            border: 2px solid #ccc;
        }

        .btn-group .btn-yes.selected .indicator {
            background: #28a745;
            border-color: #28a745;
        }

        .btn-group .btn-no.selected .indicator {
            background: #dc3545;
            border-color: #dc3545;
        }

        /* Tombol Kirim */
        .btn-submit {
            background: #007bff;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 1em;
            cursor: pointer;
            margin-top: 20px;
        }

        .btn-submit:hover {
            background: #0056b3;
        }

        /* Pesan Terima Kasih */
        .thank-you {
            margin-top: 20px;
            font-size: 1.1em;
            color: #28a745;
        }
    """),
    
    ui.div(
        {"class": "frame"},
        ui.h2("📋 Formulir Absensi Toko"),
        ui.input_text("store_id", "🏢 Kd Toko:", placeholder="Masukkan kode toko Anda"),
        ui.input_text("name", "👤 Nama Pengisi:", placeholder="Masukkan nama Anda"),
        ui.input_text("nik", "🆔 NIK:", placeholder="Masukkan NIK Anda"),
        
        ui.div(
            {"class": "radio-group"},
            ui.tags.label("🛠️ Apakah di toko ada tusukan sales draft?")
        ),
        
        ui.div(
            {"class": "btn-group"},
            ui.tags.div(
                {"class": "btn-yes"},
                ui.tags.div({"class": "indicator"}),
                ui.input_action_button("btn_yes", "✅ Ya")
            ),
            ui.tags.div(
                {"class": "btn-no"},
                ui.tags.div({"class": "indicator"}),
                ui.input_action_button("btn_no", "❌ Tidak")
            )
        ),
        
        ui.input_action_button("submit", "🚀 Kirim", class_="btn-submit"),
        ui.tags.div(ui.output_text("thank_you"), class_="thank-you"),
    ),
    
    # JavaScript untuk Indikator Bulatan
    ui.tags.script("""
        Shiny.addCustomMessageHandler('highlight', function(message) {
            let yesButton = document.querySelector('.btn-yes');
            let noButton = document.querySelector('.btn-no');
            yesButton.classList.remove('selected');
            noButton.classList.remove('selected');
            if (message.button === 'yes') {
                yesButton.classList.add('selected');
            } else if (message.button === 'no') {
                noButton.classList.add('selected');
            }
        });
    """)
)

# ----- SERVER -----
def server(input, output, session):
    selected_option = reactive.Value("")

    @reactive.Effect
    @reactive.event(input.btn_yes)
    def select_yes():
        selected_option.set("Ya")
        session.send_custom_message("highlight", {"button": "yes"})
    
    @reactive.Effect
    @reactive.event(input.btn_no)
    def select_no():
        selected_option.set("Tidak")
        session.send_custom_message("highlight", {"button": "no"})
    
    @reactive.Effect
    @reactive.event(input.submit)
    def save_response():
        data = {
            "Kd Toko": [input.store_id()],
            "Nama Pengisi": [input.name()],
            "NIK": [input.nik()],
            "Tusukan Sales Draft": [selected_option()]
        }
        df = pd.DataFrame(data)
        df.to_csv('data/responses.csv', index=False)
    
    @output
    @render.text
    def thank_you():
        return f"✅ Terima kasih, {input.name()}! Anda memilih '{selected_option()}'."

# ----- APLIKASI -----
app = App(app_ui, server)
