// sales-agent.tahamukhtar.com -> the Streamlit Community Cloud app.
// Streamlit Community Cloud doesn't support custom domains, so this domain redirects.
const TARGET = "https://sales-agent-tahamukhtar20.streamlit.app";

export default {
  fetch(request) {
    const { pathname, search } = new URL(request.url);
    // 302 so the target can change later without browsers caching the old one.
    return Response.redirect(TARGET + pathname + search, 302);
  },
};
