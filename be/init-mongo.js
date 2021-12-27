db.createUser(
  {
    user: "dsp",
    pwd: "ChangeMe",
    roles: [
      {
        role: "readWrite",
        db: "dsp_database"
      }
    ]
  }
)
