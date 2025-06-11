/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {Quiz} from "@website_slides/js/slides_course_quiz";

Quiz.include({
    async _submitQuiz() {
        // Kutsu alkuperäistä _submitQuiz-metodia
        await this._super(...arguments);

        // Päivitä slide-lista näkymä kutsumalla _refreshSlidesList-funktiota
        this._refreshSlidesList();
    },

    _refreshSlidesList() {
        const $wrapper = $(".o_wslides_fs_sidebar");
        if (!$wrapper.length) {
            console.warn("Quiz: .o_wslides_slides_list ei löytynyt.");
            return;
        }

        $.get(window.location.href, (data) => {
            const updatedContent = $(data).find(".o_wslides_fs_sidebar").html();
            if (updatedContent) {
                $wrapper.html(updatedContent);
            }
        });
    },
});
