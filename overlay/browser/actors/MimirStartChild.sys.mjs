/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Pont entre la page de demarrage et le processus parent, par evenements :
 * la page envoie « MimirStartQuery » (detail : JSON {id, name, data}) et recoit
 * « MimirStartReply » (detail : JSON {id, result}).
 */
export class MimirStartChild extends JSWindowActorChild {
  handleEvent(event) {
    if (event.type !== "MimirStartQuery") {
      return;
    }
    let request;
    try {
      request = JSON.parse(event.detail);
    } catch (e) {
      return;
    }
    if (
      typeof request.name !== "string" ||
      !request.name.startsWith("MimirStart:")
    ) {
      return;
    }
    let window = this.contentWindow;
    this.sendQuery(request.name, request.data).then(
      result => {
        window.dispatchEvent(
          new window.CustomEvent("MimirStartReply", {
            detail: JSON.stringify({ id: request.id, result }),
          })
        );
      },
      () => {}
    );
  }
}
