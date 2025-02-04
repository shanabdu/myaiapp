export async function callApi(messages: any[]) {
    const apiUrl = 'https://tamm-convai-dev-apigw.azure-api.net/conv-ai-engine/rag_search'

    const apiPayload = {
        prompt_name: 'gov-academy-course-query',
        index_configs: [
            {
                name: 'gov-academy-courses',
                number_of_results: 10,
                select_fields: [
                    'Name',
                    'Summary',
                    'Type',
                    'Skills',
                    'Language',
                    'Proficiency',
                    'Duration',
                    'URL'
                ],
                full_text_fields: ['FullText'],
                vector_fields: ['FullTextVector']
            }
        ],
        messages: messages
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-tamm-search-key': process.env.NEXT_PUBLIC_TAMM_SEARCH_KEY_GOV_ACADEMY || ''
            },
            body: JSON.stringify(apiPayload)
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        return data.data?.agent_response || 'No agent response received.'
    } catch (error) {
        console.error('API Error:', error)
        return `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
    }
}