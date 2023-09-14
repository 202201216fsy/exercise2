import sqlite3
import re
# Read the file and copy content to a list
with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = file.read().splitlines()

# Establish connection with SQLite database
conn = sqlite3.connect("stephen_king_adaptations.db")
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS stephen_kind_adaptations_table (movieID INTEGER PRIMARY KEY, movieName TEXT, movieYear INTEGER, imdbRating REAL)")

for line in stephen_king_adaptations_list:
    # 用逗号分割每一行，并去掉空格
    data = [x.strip() for x in line.split(",")]

    # 假设 data[0] = 'M01'
    data[0] = int(re.search(r'\d+', data[0]).group())

    # 检查 movieID 是否已经存在
    cursor.execute("SELECT 1 FROM stephen_kind_adaptations_table WHERE movieID = ?", (data[0],))
    if cursor.fetchone() is None:
        # 如果 movieID 不存在，插入新记录
        cursor.execute("INSERT INTO stephen_kind_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)", data)
    else:
        # 如果 movieID 已经存在，更新记录（或者选择其他操作）
        cursor.execute("UPDATE stephen_kind_adaptations_table SET movieName = ?, movieYear = ?, imdbRating = ? WHERE movieID = ?", (data[1], data[2], data[3], data[0]))

# 提交数据库的更改
conn.commit()


# Search loop
while True:
    print("\nOptions:")
    print("1. Search by Movie Name")
    print("2. Search by Movie Year")
    print("3. Search by Movie Rating")
    print("4. STOP")

    option = input("Enter your choice: ")

    if option == "1":
        movie_name = input("Enter the name of the movie: ")
        cursor.execute("SELECT * FROM stephen_kind_adaptations_table WHERE movieName=?", (movie_name,))
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            print("No such movie exists in our database.")

    elif option == "2":
        movie_year = input("Enter the year: ")
        cursor.execute("SELECT * FROM stephen_kind_adaptations_table WHERE movieYear=?", (movie_year,))
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            print("No movies were found for that year in our database.")

    elif option == "3":
        movie_rating = float(input("Enter the rating: "))
        cursor.execute("SELECT * FROM stephen_kind_adaptations_table WHERE imdbRating >= ?", (movie_rating,))
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            print("No movies at or above that rating were found in the database.")

    elif option == "4":
        break

    else:
        print("Invalid option. Please try again.")

# Close the connection
conn.close()