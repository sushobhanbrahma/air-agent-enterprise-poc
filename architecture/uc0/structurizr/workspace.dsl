workspace "UC0 - Hello Agent" "System Context and Container views for UC0" {

    !identifiers hierarchical

    model {

        u = person "Developer" "Local developer or tester interacting with UC0."

        s = softwareSystem "Air Agent Enterprise PoC" "Enterprise agentic PoC. UC0 is the minimal 'Hello Agent' use case." {
            cli = container "UC0 Hello Agent CLI" "Python" "Terminal-based chat client for local development."
            api = container "UC0 Hello Agent API" "FastAPI (Python)" "HTTP API exposing the /uc0/chat endpoint."
            llm = container "LLM Wrapper (UC0)" "Python module" "Simple wrapper around OpenAI Chat Completions API."
        }

        oa = softwareSystem "OpenAI API" "External LLM provider used for chat completions." {
            tags "External"
        }

        # Relationships
        u -> s       "Uses UC0 (via CLI and HTTP API)"
        u -> s.cli   "Types messages and reads responses"
        u -> s.api   "Sends HTTP requests (JSON)"

        s.cli -> s.llm "Sends conversation messages"
        s.api -> s.llm "Sends conversation messages"

        s.llm -> oa "Calls chat.completions" "HTTPS"
    }

    views {

        systemContext s "uc0-system-context" {
            include *
            autoLayout lr
            title "UC0 - Hello Agent - System Context"
            description "Developer interacts with the Air Agent PoC, which uses OpenAI as an external LLM provider."
        }

        container s "uc0-containers" {
            include *
            autoLayout lr
            title "UC0 - Hello Agent - Container View"
            description "CLI and FastAPI containers use a shared LLM wrapper which talks to OpenAI."
        }

        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }

            element "Software System" {
                shape RoundedBox
                background #1168bd
                color #ffffff
            }

            element "Container" {
                shape RoundedBox
                background #438dd5
                color #ffffff
            }

            element "External" {
                background #999999
                color #ffffff
            }

            relationship "Relationship" {
                color #707070
            }
        }

        themes "https://static.structurizr.com/themes/default/theme.json"
    }
}
