/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3230449310")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_o9elxaqbdm` ON `data_nasdaq_aapl` (`date`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3230449310")

  // update collection data
  unmarshal({
    "indexes": []
  }, collection)

  return app.save(collection)
})
