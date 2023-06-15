llm={}

local http=minetest.request_http_api()

local chat_logs={}

function llm.request_generation(kwargs,handler)
    http.fetch({
        url="localhost:4242",
        method="POST",
        data=kwargs,
    }, function(res)
        handler(res.data)
    end)
end
