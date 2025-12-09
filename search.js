

async function getYahooProducts(query) {
    const response = await fetch(`http://127.0.0.1:5000/scrape/Yahoo/?query=${query}`)
    const data = await response.json()
    return data
}
async function getAmiAmiProducts(query) {
    const response = await fetch(`http://127.0.0.1:5000/scrape/AmiAmi/?query=${query}`)
    const data = await response.json()
    return data
}
async function getAmiAmiProductsJP(query) {
    const response = await fetch(`http://127.0.0.1:5000/scrape/AmiAmi/JP/?query=${query}`)
    const data = await response.json()
    return data
}
async function getMandarakeProducts(query) {
    const response = await fetch(`http://127.0.0.1:5000/scrape/Mandarake/?query=${query}`)
    const data = await response.json()
    return data
}

async function getAllProducts(query) {
    productList = []
    if (/\p{Script=Hiragana}|\p{Script=Katakana}|\p{Script=Han}/u.test(query)) {
        amiItems = await getAmiAmiProductsJP(query)
    }
    else {
        amiItems = await getAmiAmiProducts(query)
    }
    
    productList = productList.concat(amiItems)
    mandaItems = await getMandarakeProducts(query)
    productList = productList.concat(mandaItems)
    yahooItems = await getYahooProducts(query)
    productList = productList.concat(yahooItems)
    return productList
}


function buildRowElements(products){
    document.querySelector("tbody").textContent = ''
    for (let i of products){
                row = document.querySelector("tbody").insertRow()
                newCell = document.createElement('th')
                newCell.scope = "row"
                image = document.createElement('img')
                image.src = i['Image']
                newCell.appendChild(image)
                row.appendChild(newCell)

                newCell = row.insertCell()
                newCell.textContent = i['Name']
                
                newCell = row.insertCell()
                newCell.textContent = i['Price']

                newCell = row.insertCell()
                image = document.createElement('img')
                image.src = i['Logo']
                newCell.appendChild(image)

                newCell = row.insertCell()
                link = document.createElement('a')
                link.href = i['Link']
                link.textContent = "Buy"
                link.target = "_blank"
                newCell.appendChild(link)
            }
}

let products = []

document.addEventListener("DOMContentLoaded", ()=>{
    
    document.querySelector("input").addEventListener("keydown", function(e){
        if (e.key == "Enter" && this.value != '') {
            products = []
            this.disabled = true
            getAllProducts(this.value).then( allItems => {
                products = allItems
                buildRowElements(products)
                this.disabled = false
            })

        }
    })




})