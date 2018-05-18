# NLPIndo

Adalah sebuah library NLP berbahasa Indonesia.

## Usage

`pip install -r requirements.txt`

Silakan baca `example.py` untuk penggunaannya.

Dikarenakan library ini hanya jalan di python, maka dibikin pula API via grpc. Silakan jalankan `grpc_server.py` dan baca `example_grpc.py` untuk penggunaannya via grpc.

## Dev

Di file `nlpindo/resource/dictionary.py` anda bisa menambahkan sendiri kata-kata baru. Begitu juga di `nlpindo/resource/stopwords.py` anda bisa menambahkan kata-kata lain yang dianggap stopwords.
