## Query Examples
`
query {
  allActors{
    edges{
      node{
        id
        name
      }
    }
  },
  allMoives{
    edges{
      node{
        id
        title
        actors {
          edges {
            node {
              id
              name
            }
          }
        },
        countryOrigin {
          id
          country
        }
      }
    }
  },
  allCountryOrigin{
    edges{
      node{
        id
        country
      }
    }
  }
  countryOrigin(id:"Q291bnRyeU9yaWdpbk5vZGU6MQ=="){
    movieSet {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
`

## Mutation Examples
`
mutation {  
  createActor(input: {
    name: "Tom Hanks"
  }) {
    ok
    actor {
      id
      name
    }
  }
}
`

`
mutation {  
  createCountryOrigin(input: {
    country: "UK"
  }) {
    ok
     countryOrigin{
      id
      country
    }
  }
}
`

`
mutation {
 createMovie(
  input: {
    title: "Ready Player Three"
    actors: [
      {
        id: "QWN0b3JOb2RlOjE="
      }
    ]
    countryOrigin: {
      id: "Q291bnRyeU9yaWdpbk5vZGU6MQ=="
    }
    year: 2017
	}) {
    ok
    movie{
      id
      title
      actors {
        edges{
          node{
            id
            name
          }
        }
      }
      year
      countryOrigin{
        id
        country
      }
    }
	}
}
`

`
mutation {
  updateMovie(
    id: "TW92aWVOb2RlOjM="
    input: {
      title: "Ready Player Two"
      actors: [
        {id: "QWN0b3JOb2RlOjE="}
      ]
      countryOrigin: {
        id: "Q291bnRyeU9yaWdpbk5vZGU6MQ=="
      }
  	}) {
    ok
    movie{
      id
      title
      actors{
        edges{
          node{
            id
            name
          }
        }
      }
      year
      countryOrigin{
        id
        country
      }
    }
  }
}
`
