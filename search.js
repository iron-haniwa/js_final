

test = [{'Name': '月姫\u3000アルクェイド\u3000雄猫堂\u3000ホビージャパン\u3000wf\u3000ガレージキット\u3000フィギュア', 'Price': 5500, 'Image': 'https://auc-pctr.c.yimg.jp/i/auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0112/user/c41e49186e349cbad1023ea9d0a7400f5f8df3668e80b7c42d74e9c0956661b0/i-img437x487-17647606731144iyytow324334.jpg?pri=l&w=300&h=300&up=0&nf_src=sy&nf_path=images/auc/pc/top/image/1.0.3/na_170x170.png&nf_st=200', 'Link': 'https://auctions.yahoo.co.jp/jp/auction/o1211037779'}]
document.addEventListener("DOMContentLoaded", ()=>{
    
    document.querySelector("input").addEventListener("keydown", function(e){
        if (e.key = "Enter") {
            for (let i of test){
                row = document.querySelector("table").insertRow()
                newCell = document.createElement('th')
                image = document.createElement('img')
                image.src = i['Image']
                newCell.appendChild(image)
                row.appendChild(newCell)

                newCell = row.insertCell()
                newCell.textContent = i['Name']
                
                newCell = row.insertCell()
                newCell.textContent = i['Price'] + " yen"

                newCell = row.insertCell()
                link = document.createElement('a')
                link.href = i['Link']
                link.textContent = "Buy"
                link.target = "_blank"
                newCell.appendChild(link)
            }
            

        }
    })




})