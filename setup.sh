# setup.sh

mkdir -p ~/.streamlit/

echo "Streamlit version: $(streamlit --version)"

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
