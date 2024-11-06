const { MongoClient, ServerApiVersion, ObjectId  } = require("mongodb");
const cors = require('cors');
require('dotenv').config();
const express = require('express');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
// TODO set up secrets for connection string

const uri = process.env.ATLAS_URI

const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
});
const database = process.env.DATABASE;
if (!database) {
    console.error('DATABASE environment variable is not set');
    process.exit(1);
}

// get to mongo connection
const myDB = client.db(database);

const MenuItems = myDB.collection("MenuItems");
const Orders = myDB.collection("Orders");



async function postMenuItems(body){
    const result = await MenuItems.insertOne(body);
    console.log(
        `new item in MenuItems created with the _id: ${result.insertedId}`,
    );
    return result.insertedId
}

app.post('/MenuItems', async (req, res) => {
    let body = req.body
  
    if (!body.name ||  !body.price ||  !body.description ) {
        return res.status(400).json({ error: 'Required fields are missing' });
    }
    
    try {
        const item = await postMenuItems(body);
        res.status(201).json({ message: 'item added successfully', item });
        return item
    } catch (error) {
        res.status(500).json({ error: 'Failed to add item' });
    }
});


async function getAllMenuItems(query={}){
    const result = await MenuItems.find(query).toArray();
    console.log("all items: ", result)
    return result   
}


app.get('/MenuItems', async (req, res) => {
    const query = req.query;
    if(query._id){
        query._id = new ObjectId(query._id)
    }

    try {
        const foundItems = await getAllMenuItems(query);
        res.status(201).json({ message: 'items grabbed', foundItems });
        return foundItems;
    } catch (error) {
        res.status(500).json({ error: 'Failed to get items' });
    }
});


async function updateMenuItems(filter, updateDoc){
    const result = await MenuItems.updateOne(filter, updateDoc);
    console.log(`${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`);
    return result
}


app.put('/MenuItems', async (req, res) => {
    const updateDoc  = {$set: req.body};
    const query = req.query

    if(query._id){
        query._id = new ObjectId(query._id)
    }

    try {
        const result = await updateMenuItems(query, updateDoc);
        res.status(200).json({ matchedCount: result.matchedCount, modifiedCount: result.modifiedCount });
    } catch (error) {
        console.log("Error: " + error)
        res.status(500).json({ error: 'Failed to update menu item' });
    }
});



async function postOrders(body){
    const result = await Orders.insertOne(body);
    console.log(
        `new item in Orders created with the _id: ${result.insertedId}`,
    );
    return result.insertedId
}

app.post('/Orders', async (req, res) => {
    let body = req.body
  
    if (!body.accountId ||  !body.orderTime ||  !body.items ||  !body.costOfItems ) {
        return res.status(400).json({ error: 'Required fields are missing' });
    }
    
    try {
        const item = await postOrders(body);
        res.status(201).json({ message: 'item added successfully', item });
        return item
    } catch (error) {
        res.status(500).json({ error: 'Failed to add item' });
    }
});


async function getAllOrders(query={}){
    const result = await Orders.find(query).toArray();
    console.log("all items: ", result)
    return result   
}


app.get('/Orders', async (req, res) => {
    const query = req.query;
    if(query._id){
        query._id = new ObjectId(query._id)
    }

    try {
        const foundItems = await getAllOrders(query);
        res.status(201).json({ message: 'items grabbed', foundItems });
        return foundItems;
    } catch (error) {
        res.status(500).json({ error: 'Failed to get items' });
    }
});


async function updateOrders(filter, updateDoc){
    const result = await Orders.updateOne(filter, updateDoc);
    console.log(`${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`);
    return result
}


app.put('/Orders', async (req, res) => {
    const updateDoc  = {$set: req.body};
    const query = req.query

    if(query._id){
        query._id = new ObjectId(query._id)
    }

    try {
        const result = await updateOrders(query, updateDoc);
        res.status(200).json({ matchedCount: result.matchedCount, modifiedCount: result.modifiedCount });
    } catch (error) {
        console.log("Error: " + error)
        res.status(500).json({ error: 'Failed to update menu item' });
    }
});




app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
