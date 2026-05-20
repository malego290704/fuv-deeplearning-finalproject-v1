/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3230449310")

  // update collection data
  unmarshal({
    "name": "data_nasdaq_aapl"
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3230449310")

  // update collection data
  unmarshal({
    "name": "data_nasdaq_appl"
  }, collection)

  return app.save(collection)
})
