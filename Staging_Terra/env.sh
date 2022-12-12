cat outputs.txt > .env
sql_uri=$(cat outputs.txt | sed '2!d')
echo "$sql_uri"
export DB_URI="'${sql_uri}'"
