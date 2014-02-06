#include "eossocialutils.h"

#include <libsoup/soup.h>

typedef struct {
  EosSocialLoadFailedCallback callback;
  gpointer user_data;
} LoadFailedData;

static void
load_failed_data_free (gpointer _data)
{
  LoadFailedData *data = _data;
  g_slice_free (LoadFailedData, data);
}

static gboolean
on_load_failed (WebKitWebView *web_view,
                WebKitLoadEvent load_event,
                gchar *failing_uri,
                GError *error,
                gpointer user_data)
{
  LoadFailedData *data = user_data;
  gboolean res = FALSE;

  if (error->domain == SOUP_HTTP_ERROR ||
      error->code == WEBKIT_NETWORK_ERROR_FAILED ||
      error->code == WEBKIT_NETWORK_ERROR_TRANSPORT ||
      error->code == WEBKIT_NETWORK_ERROR_UNKNOWN_PROTOCOL ||
      error->code == WEBKIT_NETWORK_ERROR_FILE_DOES_NOT_EXIST ||
      error->code == WEBKIT_POLICY_ERROR_FAILED ||
      error->code == WEBKIT_POLICY_ERROR_CANNOT_SHOW_MIME_TYPE ||
      error->code == WEBKIT_POLICY_ERROR_CANNOT_SHOW_URI ||
      error->code == WEBKIT_POLICY_ERROR_CANNOT_USE_RESTRICTED_PORT ||
      error->code == WEBKIT_PLUGIN_ERROR_FAILED ||
      error->code == WEBKIT_PLUGIN_ERROR_CANNOT_FIND_PLUGIN ||
      error->code == WEBKIT_PLUGIN_ERROR_CANNOT_LOAD_PLUGIN ||
      error->code == WEBKIT_PLUGIN_ERROR_JAVA_UNAVAILABLE ||
      error->code == WEBKIT_PLUGIN_ERROR_CONNECTION_CANCELLED)
    {
      data->callback (web_view, load_event, failing_uri, error, data->user_data);
      res = TRUE;
    }

  return res;
}

/**
 * eos_social_connect_to_load_failed:
 * @web_view:
 * @callback: (scope async):
 * @user_data: (closure):
 */
void
eos_social_connect_to_load_failed (WebKitWebView *web_view,
                                   EosSocialLoadFailedCallback callback,
                                   gpointer user_data)
{
  LoadFailedData *data = g_slice_new0 (LoadFailedData);
  data->callback = callback;
  data->user_data = user_data;

  g_object_set_data_full (G_OBJECT (web_view),
                          "load-failed-data", data,
                          load_failed_data_free);

  g_signal_connect (web_view, "load-failed",
                    G_CALLBACK (on_load_failed), data);
}
