import engine
import pypandoc

x = input("introduce an url: ")
print("scraping book")
book = engine.metadataBookExtractor(x)

# Opening/Creating HTML file
file = open(book.title + ".html", 'w', encoding='utf-8')

file.write(f"<html><head>\
	        <meta name='title' content='{book.title}'>\
	        </head><body>")

# Adding separate cover image, so that it shows in HTML
file.write("<div style=text-align:center;>\
			<img src=" + "" + " alt='cover_image'>\
			</div>")

file.write("<br><br>" + book.description + "<br>")
file.write(
    "<br><br><div<br>* Converted using bukku by arnxxau<br></h6></div>")

for chapter in book.chapters:
    file.write("<br><br><h2>" + chapter.name + "'</h2><br><br>")
    print("writing " + chapter.name)

    for line in chapter.content:
        file.write(line + "<br>")

file.write("</body></html>")
file.close()
print("creating epub, please wait")
output = pypandoc.convert_file(book.title + ".html", 'epub3', outputfile=book.title + ".epub",
                               extra_args=['--epub-chapter-level=2'])
assert output == ""
