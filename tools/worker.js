// One canonical host: www and any http request move permanently to https://xlunastudio.com.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname !== "xlunastudio.com" || url.protocol !== "https:") {
      url.hostname = "xlunastudio.com";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
